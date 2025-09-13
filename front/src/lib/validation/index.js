import { z } from "zod";

export const SignupValidation = z.object({
  name: z.string().min(2, {message: "Nome deve ter no mínimo 2 caracteres"}),
  username: z.string().min(2, {message: "Username deve ter no mínimo 2 caracteres"}),
  email: z.string().email({message: "Email inválido"}),
  password: z.string().min(8, {message: "Senha deve ter no mínimo 6 caracteres"})
});

export const SigninValidation = z.object({
  email: z.string().email({message: "Email inválido"}),
  password: z.string().min(8, {message: "Senha deve ter no mínimo 6 caracteres"})
});