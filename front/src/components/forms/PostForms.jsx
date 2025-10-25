import * as z from "zod"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { useNavigate } from "react-router-dom"
 

import { Button } from "@/components/ui/button"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

import { Textarea } from "../ui/textarea"
import { Input } from "../ui/input"
import UploadImage from "../shared/UploadImage"


const formSchema = z.object({
  caption: z.string().min(2, {
    message: "Descrição deve ter no mínimo 2 caracteres.",
  }),
})

const PostForms = () => {
    const navigate = useNavigate();

    const form = useForm({
        resolver: zodResolver(formSchema),
        defaultValues: {
        caption: "",
        },
    })


    function onSubmit(values) {

        console.log(values)
    }

    function handleCancel() {
        navigate(-1)
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-9 w-full max-w-5xl">
                <FormField
                control={form.control}
                name="Descrição"
                render={({ field }) => (
                <FormItem>
                    <FormLabel className="shad-form_label">Descrição</FormLabel>
                    <FormControl>
                        <Textarea className="shad-textarea custom-scrollbar rounded-xl" {...field} />
                    </FormControl>
                    <FormDescription>
                        Essa é a descrição do seu post.
                    </FormDescription>
                    <FormMessage className="shad-form_message" />
                </FormItem>
                )}
                />
                <FormField
                    control={form.control}
                    name="Foto"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel className="shad-form_label">Adicionar foto</FormLabel>
                        <FormControl>
                            
                            <UploadImage />

                        </FormControl>
                        <FormDescription>
                            Essa é a foto ao seu post.
                        </FormDescription>
                        <FormMessage className="shad-form_message" />
                </FormItem>
                )}
                />
                <FormField
                    control={form.control}
                    name="Localização"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel className="shad-form_label">Adicionar localização</FormLabel>
                        <FormControl>
                            <Input className="shad-input rounded-xl" placeholder="Adicione sua localização ao post." {...field} />
                        </FormControl>
                        <FormDescription>
                            Essa é seu local.
                        </FormDescription>
                        <FormMessage className="shad-form_message" />
                </FormItem>
                )}
                />
                <FormField
                    control={form.control}
                    name="Tags"
                    render={({ field }) => (
                        <FormItem>
                        <FormLabel className="shad-form_label">Adicionar Tags (separadas por ",") </FormLabel>
                        <FormControl>
                            <Input type = "text" className="shad-input rounded-xl" placeholder="é u dudu" {...field} />
                        </FormControl>
                        <FormDescription>
                            Essas são as tags do seu post.
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
                    >
                        Cancelar
    
                    </Button>

                    <Button 
                        type="submit" 
                        className="shad-button_primary rounded-xl"
                    >
                        Enviar
    
                    </Button>

                </div>
            </form>
        </Form>
  )

}

export default PostForms