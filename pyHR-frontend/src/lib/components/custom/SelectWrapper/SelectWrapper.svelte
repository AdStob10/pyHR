<script lang="ts">
import * as Select from "$lib/components/ui/select"
	import { cn } from "$lib/utils";
	import type { Icon } from "@lucide/svelte";
	import type { ClassValue } from "clsx";
	import type { Component } from "svelte";
	import { defaultValues } from "sveltekit-superforms";



export type SelectOption = {
    label: string
    value: any
    icon: Component 
    | undefined 
}
export type SelectProps = {
    options: SelectOption[]
    selectedOption?: SelectOption | undefined
    onValueChangeFn: (val: any) => void
    placeholder?: string,
    classValues?: ClassValue[]
    name?: string
}
let {options, selectedOption, placeholder, onValueChangeFn, classValues, name}: SelectProps = $props()



</script>

<Select.Root name={name} type="single" onValueChange={onValueChangeFn} value={selectedOption?.value}>
    <Select.Trigger class={cn(classValues)}>
        {#if selectedOption}
            {@const Icon = selectedOption.icon}
            {#if Icon}
                <Icon class="mr-1 w-4 h-4"/>  {selectedOption.label}
            {:else}
                 {selectedOption.label}
            {/if}
        {:else}
            {placeholder}
        {/if}
    </Select.Trigger>
    <Select.Content>
        {#each options as option (option.value)}
            {@const Icon = option.icon}
            {#if Icon}
                <Select.Item value={option.value}><Icon class="mr-2 w-4 h-4"/> {option.label}</Select.Item>
            {:else}
                <Select.Item value={option.value}>{option.label}</Select.Item>
            {/if}
        {/each}
    </Select.Content>
</Select.Root>