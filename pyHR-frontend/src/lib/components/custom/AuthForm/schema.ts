import { z } from "zod";


export const authFormSchema = z.object({
    username: z.string({
        required_error:"Login jest wymagany",
    })
    .min(3, "Login musi mieć minimum 3 znaki")
    .max(50, "Login może mieć maksymalnie 50 znaków"),
    password: z.string({
        required_error:"Login jest wymagany",
    })
    .min(3, "Hasło musi mieć minimum 3 znaki")
    .max(50, "Login może mieć maksymalnie 50 znaków")
})

export type AuthFormSchema = typeof authFormSchema;