import type { Role } from '$lib/utils/objects';

type PaginatedList<T> = {
	data: T[];
	rowCount: number;
};

type TokenData = {
	access_token: string;
	token_type: string;
};

type UserData = {
	id: number;
	username: string;
	firstName: string;
	lastName: string;
	role: number;
	email: string | undefined;
};

type UserWithRole = Omit<UserData, 'role'> & {
	role: Role;
};

type VacationRequest = {
	id: number;
	startDate: string;
	endDate: string;
	reason: string | null;
	status: intger | null;
	vacationType: VacationType;
};

type VacationType = {
	id: number;
	name: string;
	description: string;
};

type Employee = Omit<UserData, { role: number; email: string }>;
type EmployeeDetails = UserData & {
	jobTitle: string
	employmentDate: date,
	department: string
}
type EmployeeDetailsWithManager = EmployeeDetails & {
	manager: EmployeeDetails
}

type AvailableVacation = {
	employeeId: number;
	vacationTypeId: number;
	availableDays: number;
	vacationType: VacationType;
};

type VacationInMonth = {
	month: number;
	acceptedDays: number;
	newDays: number;
	rejectedDays: number;
};


type VacationInMonthChartData = {
	month: string;
	acceptedDays: number;
	newDays: number;
	rejectedDays: number;
};

type SubordinateVacationRequest = VacationRequest & {
	employee: Employee;
};

export type {
	PaginatedList,
	TokenData,
	UserData,
	VacationRequest,
	VacationType,
	AvailableVacation,
	UserWithRole,
	SubordinateVacationRequest,
    VacationInMonth,
	VacationInMonthChartData,
	EmployeeDetailsWithManager
};
