<script lang="ts">
import * as Select from "$lib/components/ui/select"
	import type { Icon } from "@lucide/svelte";
	import type { FilterItem } from "./filtersUtils";
	import type { Component } from "svelte";
	import type { SelectProps } from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte";
	import SelectWrapper from "$lib/components/custom/SelectWrapper/SelectWrapper.svelte";
	import type { ClassValue } from "clsx";


type FilterSelectProps = SelectProps & {
    selected: FilterItem
	classValues?: ClassValue[]
}
let props : FilterSelectProps = $props()

let selectedOption = $derived(props.options.find(s => s.value === props.selected.value))

</script>
<div class="flex-col justify-items-center gap-2">
    <h4 class="text-muted-foreground mb-2">{props.selected.label}</h4>
<SelectWrapper {...props} {selectedOption}  />
</div>