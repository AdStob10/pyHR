


import { getLocalTimeZone, parseDate, today } from '@internationalized/date'
import { z } from 'zod'

export type StringDateRange = {
    startDate: string,
    endDate: string
}

const range = z.object({
   startDate: z.string({required_error: "Data końcowa musi być podana"}),
   endDate: z.string({required_error: "Data końcowa musi być podana"})
}).superRefine((val, ctx) => {
    if (!val) {
        ctx.addIssue({code:"custom", message:"Zakres jest wymagany"})
        return
    }
    if (!val.startDate) {
        ctx.addIssue({code:"custom", message:"Data początkowa wymagana"})
        return;
    }
    if (!val.endDate) {
        ctx.addIssue({code:"custom", message:"Data "})
        return
    }


    const startDate = parseDate(val.startDate)
    const todayDate = today(getLocalTimeZone())
    if (startDate.compare(todayDate) < 0 ) ctx.addIssue({code:"custom", message:"Data nie może być w przeszłości !"})

})



export const addRequestSchema = z.object({
    vacationTypeId: z.number({required_error:"Rodzaj urlopu jest wymagany"})
                    .min(1, "Proszę wybrać rodzaj urlopu"),
    dateRange: range,
    reason: z.string().max(200, "Powód powinien mieć maksimum 200 znaków").optional()
})


export type AddRequestSchema = typeof addRequestSchema