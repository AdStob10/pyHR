
import { z } from 'zod'



export const addEmployeeSchema = z.object({
    username: z.string()
    .max(100, "Nazuwa użytkownika powinna mieć maksymalnie 100 znaków")
    .min(3, "Nazwa użytkownika powinna mieć przynajmniej 3 znaki"),

    password: z.string()
    .max(100, "Hasło powinno mieć maksymalnie 100 znaków")
    .min(3, "Hasło powinno mieć przynajmniej 3 znaki")
    .regex(/^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]).{8,}$/,
            "Hasło musi mieć przynajmniej jedną dużą literę, jedną cyfrę i jeden znak specjalny"
    ),

    firstName: z.string()
    .max(150, "Imię powinno mieć maksymalnie 150 znaków")
    .min(2, "Imię powinno mieć przynajmniej 2 znaki"),

    lastName: z.string()
    .max(150, "Imię powinno mieć maksymalnie 150 znaków")
    .min(2, "Imię powinno mieć przynajmniej 2 znaki"),

    employmentDate: z.string({required_error: "Data zatrudnienia musi być podana"}),

    jobTitle: z.string()
    .max(150, "Stanowisko powinno mieć maksymalnie 150 znaków")
    .optional(),

    department: z.string()
    .max(150, "Oddział powinnen mieć maksymalnie 150 znaków")
    .optional(),

    
})


export type AddEmployeeSchema = typeof addEmployeeSchema