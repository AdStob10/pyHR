import type { FilterItem } from "../utils/Filters/filtersUtils";

export const initialFilters: Record<string, FilterItem> = {
    status: {
        label: "Status",
        name: "status",
        value: undefined,
    },
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
    startDate: {
        label: "Początek",
        name: "start_date",
        value: undefined,
        type: "eq"
    },
    endDate: {
        label: "Koniec",
        name: "end_date",
        value: undefined,
        type: "eq"
    },
    vacationType: {
        label: "Rodzaj urlopu",
        name: "vacation_type_id",
        value: undefined,
    }
}
