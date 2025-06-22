import { z } from "zod";


export const authFormSchema = z.object({
    username: z.string({
        required_error:"Login jest wymagany",
    })
    .min(3, "Login musi mieć minimum 3 znaki")
    .max(100, "Login może mieć maksymalnie 100 znaków"),

    
    password: z.string({
        required_error:"Hasło jest wymagane",
    })
})

export type AuthFormSchema = typeof authFormSchema;