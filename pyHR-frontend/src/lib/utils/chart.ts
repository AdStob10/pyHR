import type { AvailableVacation, VacationInMonth, VacationInMonthChartData, VacationType } from "$lib/types";

const monthNames = [
  "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec",
  "lipiec", "sierpień", "wrzesień", "październik", "listopad", "grudzień"
];



export type AvailableVacationChartData = {
 type: string,
 days: number,
 color: string   
}

const mapAvailableVacationToChartData = (availableVacation: AvailableVacation[]) => {
    return availableVacation.map((av, i) => {
        return {
            type: av.vacationTypeId.toString(), 
            days: av.availableDays,
            color: `var(--chart-${i+1})`
        } satisfies AvailableVacationChartData
    })
}  


const mapVacationTypesToChartConfig = (vacationTypes: VacationType[]) => {
    const config = {}
    let i = 1
    for (const type of vacationTypes) {
        Object.defineProperty(config, type.id, {
            value: {
                label: type.name,
                color: `var(--chart-${i})`
            }
        })
        i+=1
    }

    // console.log(config)
    return config;
}

const mapVacationMonthlyToChartData = (vacationsMonthly: VacationInMonth[]) => {
    return vacationsMonthly.map(({month, acceptedDays, rejectedDays, newDays}) => 
        ({month: monthNames[month], acceptedDays, rejectedDays, newDays} satisfies VacationInMonthChartData)
    )
}

export {mapAvailableVacationToChartData, mapVacationTypesToChartConfig, mapVacationMonthlyToChartData}