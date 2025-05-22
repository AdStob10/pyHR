type PaginatedList<T> = {
    data: T[],
    rowCount: number
}


type TokenData = {
    access_token: string
    token_type: string
}

type UserData = {
    id: number,
    username: string,
    email: string | undefined
}


type VacationRequest = {
    id: number,
    startDate: string,
    endDate: string,
    reason: string | null,
    status: intger | null,
    vacationType: VacationType
}

type VacationType = {
    id: number,
    name: string,
    description: string
}



type AvailableVacation = {
    employeeId: number,
    vacationTypeId: number,
    availableDays: number,
    vacationType: VacationType
}


export type {PaginatedList, TokenData, UserData, VacationRequest, VacationType, AvailableVacation}