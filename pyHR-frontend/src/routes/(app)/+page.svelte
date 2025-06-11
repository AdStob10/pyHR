<script lang="ts">
	import AvailableDaysChart from "$lib/components/charts/AvailableDaysChart.svelte";
	import VacationsMonthlyChart from "$lib/components/charts/VacationsMonthlyChart.svelte";
	import type { PageProps } from "./$types";

    let { data }: PageProps = $props()

</script>


<AvailableDaysChart availableDays={data.availableDays} vacationTypes={data.vacationTypes} />
<VacationsMonthlyChart data={data.vacationInMonth} />