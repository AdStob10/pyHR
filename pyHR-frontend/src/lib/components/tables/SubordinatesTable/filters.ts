import type { FilterItem } from "../utils/Filters/filtersUtils";

export const initialFilters: Record<string, FilterItem> = {
    firstName: {
        label: "Imię",
        name: "first_name",
        value: undefined,
    },
    lastName: {
        label: "Nazwisko",
        name: "last_name",
        value: undefined,
    },
    jobTitle: {
        label: "Stanowisko",
        name: "job_title",
        value: undefined,
    },
    department: {
        label: "Dział",
        name: "department",
        value: undefined
    },
    employmentDate: {
        label: "Data zatrudnienia",
        name: "employment_date",
        value: undefined,
        type: "eq"
    },
}