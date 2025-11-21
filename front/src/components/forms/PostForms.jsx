import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";
import { createPost } from "../../api";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

import { Textarea } from "../ui/textarea";
import UploadImage from "../shared/UploadImage";

const formSchema = z.object({
  caption: z.string().min(2, {
    message: "Descrição deve ter no mínimo 2 caracteres.",
  }),
});

const PostForms = () => {
  const navigate = useNavigate();
  const { artistId } = useParams();
  const [selectedImages, setSelectedImages] = useState([]);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: {
      caption: "",
    },
  });

  async function onSubmit(values) {
    setIsSubmitting(true);

    try {
      const result = await createPost(artistId, values.caption, selectedImages);

      if (result.success) {
        console.log("Post criado com sucesso!", result.data);
        navigate(`/artist/${artistId}`);
      } else {
        console.error("Erro ao criar post:", result.error);
        alert(`Erro ao criar post: ${result.error}`);
      }
    } catch (error) {
      console.error("Erro ao criar post:", error);
      alert("Erro ao criar post");
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleCancel() {
    navigate(-1);
  }

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="flex flex-col gap-9 w-full max-w-5xl"
      >
        <FormField
          control={form.control}
          name="caption"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="shad-form_label">Descrição</FormLabel>
              <FormControl>
                <Textarea
                  className="shad-textarea custom-scrollbar rounded-xl"
                  {...field}
                />
              </FormControl>
              <FormDescription>Essa é a descrição do seu post.</FormDescription>
              <FormMessage className="shad-form_message" />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="images"
          render={({ field }) => (
            <FormItem>
              <FormLabel className="shad-form_label">Adicionar foto</FormLabel>
              <FormControl>
                <UploadImage
                  selectedImages={selectedImages}
                  setSelectedImages={setSelectedImages}
                />
              </FormControl>
              <FormDescription>
                Adicione fotos ao seu post (opcional).
              </FormDescription>
              <FormMessage className="shad-form_message" />
            </FormItem>
          )}
        />

        <div className="flex justify-end gap-4">
          <Button
            type="button"
            onClick={handleCancel}
            className="shad-button_dark rounded-xl"
            disabled={isSubmitting}
          >
            Cancelar
          </Button>

          <Button
            type="submit"
            className="shad-button_primary rounded-xl"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Enviando..." : "Publicar"}
          </Button>
        </div>
      </form>
    </Form>
  );
};

export default PostForms;
