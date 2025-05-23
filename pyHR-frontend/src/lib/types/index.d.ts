import type { Role } from "$lib/utils/objects"

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
    firstName: string,
    lastName: string,
    role: number,
    email: string | undefined
}

type UserWithRole = Omit<UserData, 'role'> & {
    role: Role
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


type Employee = Omit<UserData, {role: number, email: string}> 



type AvailableVacation = {
    employeeId: number,
    vacationTypeId: number,
    availableDays: number,
    vacationType: VacationType
}

type SubordinateVacationRequest = VacationRequest & {
    employee: Employee
}

export type {PaginatedList, TokenData, UserData, VacationRequest, VacationType, AvailableVacation, UserWithRole, SubordinateVacationRequest}