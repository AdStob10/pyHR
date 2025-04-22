<script lang="ts">
    import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
    import { Button } from '$lib/components/ui/button';
    import SuperDebug, { superForm, type Infer, type SuperValidated } from "sveltekit-superforms";
	import { zodClient } from "sveltekit-superforms/adapters";
	import { authFormSchema, type AuthFormSchema } from "./schema";
	import { LoaderCircle } from '@lucide/svelte';

    let { data } : {data: SuperValidated<Infer<AuthFormSchema>>} = $props();
 
    const form = superForm(data, {
        validators: zodClient(authFormSchema)
    });


    const { form: formData, enhance, delayed, message } = form;
</script>

<SuperDebug data={$formData} />
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
        <Form.Field {form} name="username">
            <Form.Control let:attrs>
                <Form.Label >Nazwa użytkownika</Form.Label>
                <Input {...attrs} bind:value={$formData.username}/>
            </Form.Control>
            <Form.FieldErrors />
        </Form.Field>
        <Form.Field {form} name="password">
            <Form.Control let:attrs>
                <Form.Label>Hasło</Form.Label>
                <Input {...attrs} bind:value={$formData.password}/>
            </Form.Control>
            <Form.FieldErrors />
        </Form.Field>
        <div class="flex">
            <Form.Button class="flex-1" disabled={$delayed} type="submit" variant="outline">
                {#if $delayed}
                    <LoaderCircle class="mr-2 h-4 w-4 animate-spin" />
                    Proszę czekać
                {:else}
                    Zaloguj się
                {/if}
            </Form.Button>
        </div>

</div>
</form>

