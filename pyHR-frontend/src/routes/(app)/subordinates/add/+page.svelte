<script lang="ts">
	import AddEmployeeForm from "$lib/components/custom/Forms/AddEmployee/AddEmployeeForm.svelte";
	import type { PageProps } from "./$types";


let { data }: PageProps = $props();
</script>

<div class="flex justify-center">
    <AddEmployeeForm data={data.form} />
</div>