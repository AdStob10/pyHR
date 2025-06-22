<script lang="ts">
	import SuperDebug, { superForm, type Infer, type SuperValidated } from "sveltekit-superforms";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { addEmployeeSchema, type AddEmployeeSchema } from "./schema";
	import * as Card from "$lib/components/ui/card";
	import { buttonVariants } from "$lib/components/ui/button";
	import { cn } from "$lib/utils";
    import * as Form from '$lib/components/ui/form';
	import { LoaderCircle } from "@lucide/svelte";
	import { Input } from "$lib/components/ui/input";
	import { dev } from "$app/environment";
	import FormDatePicker from "$lib/components/utils/FormDatePicker.svelte";

    type AddEmployeeFormProps = {
        data: SuperValidated<Infer<AddEmployeeSchema>>,
    }

    let { data } : AddEmployeeFormProps = $props();


    const form = superForm(data, {
    dataType: "json",
    validators: zodClient(addEmployeeSchema)
    });

    const { form: formData, enhance, delayed, message } = form;

</script>


<Card.Root class="p-4">
    <SuperDebug data={$formData} display={dev} collapsible />
    <form method="POST" use:enhance>
    <Card.Header>
      <Card.Title>Nowy pracownik</Card.Title>
    </Card.Header>
    <Card.Content>
        <div class="grid gap-6 text-center">
            {#if $message}
                    <div 
                class:text-destructive={$message.status == "error"}
                class:text-primary={$message.status == "success"}
                >
                    {$message.text}
                </div>
            {/if}
            <Form.Field {form} name="username">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Nazwa użytkownika</Form.Label>
                    <Input {...props} bind:value={$formData.username}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="password">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Hasło</Form.Label>
                    <Input type="password" {...props} bind:value={$formData.password}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <div class="flex gap-3">
            <Form.Field {form} name="firstName">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Imię</Form.Label>
                    <Input {...props} bind:value={$formData.firstName}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="lastName">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Nazwisko</Form.Label>
                    <Input {...props} bind:value={$formData.lastName}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            </div>    
            <Form.Field {form} name="jobTitle">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Stanowisko</Form.Label>
                    <Input {...props} bind:value={$formData.jobTitle}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="department">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Dział</Form.Label>
                    <Input {...props} bind:value={$formData.department}/>
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
            <Form.Field {form} name="employmentDate">
                <Form.Control>
                {#snippet children({ props })}
                    <Form.Label >Data Zatrudnienia</Form.Label>
                    <FormDatePicker {...props} bind:value={$formData.employmentDate} />
                {/snippet}
                </Form.Control>
                <Form.FieldErrors />
            </Form.Field>
        </div>
    </Card.Content>
        <Card.Footer>
            <div class="flex grow mt-2">
                <Form.Button class="w-full" disabled={$delayed} type="submit" variant="outline">
                    {#if $delayed}
                        <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
                        Proszę czekać
                    {:else}
                        Dodaj
                    {/if}
                </Form.Button>
            </div>
        </Card.Footer>
        </form>
</Card.Root>