<script lang="ts">
	import * as Select from "$lib/components/ui/select";
	import DatePicker from "$lib/components/utils/DatePicker.svelte";
	import type { DateValue } from "@internationalized/date";
	import { filterTypes, type FilterItem, type FilterType } from "./filtersUtils";
	import FilterSelect from "./FilterSelect.svelte";
	import SelectWrapper from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte";

    type FilterDateProps = {
        filter: FilterItem,
        onValueChangeFn: (val: DateValue | undefined) => void
        onTypeChangeFn: (val: FilterType) => void
    }


    let { filter, onValueChangeFn, onTypeChangeFn }: FilterDateProps = $props();
    let selectedOption = $derived(filterTypes.find(s => s.value === filter.type))

</script>
<div class="flex-col justify-items-center gap-2">
    <h4 class="text-muted-foreground mb-2">{filter.label}</h4>
    <div class="gap-2 justify-items-center flex">
        <div>
        <SelectWrapper 
            options={filterTypes} 
            {selectedOption} 
            onValueChangeFn={onTypeChangeFn} 
            placeholder={"Filtruj..."}
            classValues={["w-[100px]"]}
        />
        </div>
        <DatePicker value={filter.value as DateValue | undefined} {onValueChangeFn} />
    </div>
</div>