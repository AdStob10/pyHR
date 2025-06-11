<script lang="ts">
	import { buttonVariants } from "$lib/components/ui/button/button.svelte";
	import * as Dialog from "$lib/components/ui/dialog";
	import * as Form from '$lib/components/ui/form';
	import { Textarea } from "$lib/components/ui/textarea";
	import RangeDatePicker from "$lib/components/utils/RangeDatePicker.svelte";
	import type { AvailableVacation } from "$lib/types";
	import { cn } from "$lib/utils";
	import { LoaderCircle } from "@lucide/svelte";
	import SuperDebug, { superForm, type Infer, type SuperValidated } from "sveltekit-superforms";
	import { zodClient } from "sveltekit-superforms/adapters";
	import SelectWrapper, { type SelectOption } from "../SelectWrapper/SelectWrapper.svelte";
	import { addRequestSchema, type AddRequestSchema } from "./schema";
    import { dev } from '$app/environment';
	
    type AddRequestFormProps = {
        data: SuperValidated<Infer<AddRequestSchema>>,
        availableDays: AvailableVacation[]
    }

    let { data, availableDays } : AddRequestFormProps = $props();
    
    const form = superForm(data, {
        dataType: "json",
        validators: zodClient(addRequestSchema)
    });
    
    const { form: formData, enhance, delayed, message } = form;
    const options = $derived.by(() => 
        availableDays
        .filter(ad => ad.availableDays > 0)
        .map(ad => ({label: ad.vacationType.name, value: ad.vacationType.id} as SelectOption))
    )
    const selectedOption = $derived(options.find(o => o.value == $formData.vacationTypeId))
    const selectedAvailableVacation = $derived(availableDays.find(ad => ad.vacationTypeId == $formData.vacationTypeId))

</script>


<Dialog.Root>
  <Dialog.Trigger class={cn(buttonVariants({ variant: "default" }), "w-[10rem] mb-5")}>Nowy wniosek</Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Nowy wniosek urlopowy</Dialog.Title>
    </Dialog.Header>
        <SuperDebug data={$formData} display={dev} collapsible />
        <form method="POST" use:enhance>
        <div class="grid gap-6 text-center">
            {#if $message}
                    <div 
                class:text-destructive={$message.status == "error"}
                class:text-primary={$message.status == "success"}
                >
                    {$message.text}
                </div>
            {/if}
            {#if selectedAvailableVacation !== undefined}
                <div>Dostępne dni: {selectedAvailableVacation.availableDays}</div>
            {/if}
            <Form.Field {form} name="dateRange">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Okres urlopu</Form.Label>
                    <RangeDatePicker {...props} bind:start={$formData.dateRange.startDate} bind:end={$formData.dateRange.endDate}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
             <Form.Field {form} name="vacationTypeId">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Rodzaj Urlopu</Form.Label>
                    <SelectWrapper 
                        {...props} 
                        options={options} 
                        selectedOption={selectedOption} 
                        onValueChangeFn={(val: any) => $formData.vacationTypeId = val}
                    />
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="reason">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Powód</Form.Label>
                    <Textarea {...props} bind:value={$formData.reason}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
        </div>
        <Dialog.Footer>
            <div class="flex">
                <Form.Button class="flex-1" disabled={$delayed} type="submit" variant="outline">
                    {#if $delayed}
                        <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
                        Proszę czekać
                    {:else}
                        Dodaj
                    {/if}
                </Form.Button>
            </div>
        </Dialog.Footer>
        </form>
  </Dialog.Content>
</Dialog.Root>