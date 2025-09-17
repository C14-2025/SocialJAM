import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigate } from "react-router-dom";

import { Button } from "@/components/ui/button";
import { useForm } from "react-hook-form";
import { useState } from "react";

import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { SigninValidation } from "@/lib/validation";
import Loader from "@/components/shared/Loader";
import { loginUser } from "@/api";
import { useAuth } from "@/context/AuthContext";



const SigninForms = () => {
  const [isUserLoading, setIsUserLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();


  const form = useForm({
    resolver: zodResolver(SigninValidation),
    defaultValues: {
      email: "",
      password: "",
    },
  });


  async function onSubmit(values) {
    console.log(values);
    setIsUserLoading(true);
    setErrorMessage("");

    try {
      const result = await loginUser(values.email, values.password);
      
      if (result.success) {
        login();
        navigate("/");
      } else {
        setErrorMessage(result.error);
      }
    } catch (error) {
      console.error('Erro no login:', error);
      setErrorMessage("Erro inesperado. Tente novamente.");
    } finally {
      setIsUserLoading(false);
    }
  }
  return (  
    <Form {...form}>
      <div className="sm:w-420 flex-center flex-col">
        <img src = "/assets/images/logo.svg" alt = "logo"/> 

        <h2 className="h3-bold md:h2-bold pt-5 sm:pt-12">Entre com sua conta</h2>

        <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col gap-5 w-full mt-4">
          
          {errorMessage && (
            <div className="bg-red-500/20 text-red-500 p-3 rounded-xl text-center">
              {errorMessage}
            </div>
          )}

          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input type="email" className="shad-input rounded-xl" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Senha</FormLabel>
                <FormControl>
                  <Input type="password" className="shad-input rounded-xl" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" 
          className="shad-button_primary rounded-xl">
            {isUserLoading ?(
              <div className="flex-center gap-2 rounded-xl">
                <Loader /> Carregando...
              </div>
            ) : (
              "Enviar"
            )}
          </Button>
          <p className="text-small-regular text-light-2 text-center mt-2 rounded-xl">
            Não possui uma conta?
            <Link to="/signup" className="text-primary-500 text-small-semibold ml-1 rounded-xl">
              Crie uma conta
            </Link>
          </p>
        </form>
      </div>
    </Form>
    
  );
};

export default SigninForms;
