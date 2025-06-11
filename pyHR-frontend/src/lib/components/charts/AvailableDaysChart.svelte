<script lang="ts">
	import type { AvailableVacation, VacationType } from "$lib/types";
	import { mapAvailableVacationToChartData, mapVacationTypesToChartConfig } from "$lib/utils/chart";
	import { getLocalTimeZone, today } from "@internationalized/date";
	import * as Card from "../ui/card";
	import * as Chart from "../ui/chart";
    import { PieChart, Text } from "layerchart";

    type AvailableDaysChartProps = {
        availableDays: AvailableVacation[],
        vacationTypes: VacationType[]
    }

    let { availableDays, vacationTypes }: AvailableDaysChartProps = $props()

    
    const chartData = mapAvailableVacationToChartData(availableDays)
    const chartConfig = mapVacationTypesToChartConfig(vacationTypes) as Chart.ChartConfig
    const todayDate = today(getLocalTimeZone())

    const totalDays = chartData.reduce((acc, curr) => acc + curr.days, 0);
</script>


<Card.Root class="flex flex-col">
	<Card.Header class="items-center">
		<Card.Title>Dostępne dni urlopu</Card.Title>
		<Card.Description>Rok {todayDate.year}</Card.Description>
	</Card.Header>
	<Card.Content class="flex-1">
		<Chart.Container config={chartConfig} class="mx-auto aspect-square max-h-[250px]">
			<PieChart
				data={chartData}
				key="type"
				value="days"
				c="color"
				innerRadius={60}
				padding={28}
				props={{ pie: { motion: "tween" } }}
			>
				{#snippet aboveMarks()}
					<Text
						value={String(totalDays)}
						textAnchor="middle"
						verticalAnchor="middle"
						class="fill-foreground text-3xl! font-bold"
						dy={3}
					/>
					<Text
						value="Dni"
						textAnchor="middle"
						verticalAnchor="middle"
						class="fill-muted-foreground! text-muted-foreground"
						dy={22}
					/>
				{/snippet}
				{#snippet tooltip()}
					<Chart.Tooltip hideLabel  />
				{/snippet}
			</PieChart>
		</Chart.Container>
	</Card.Content>
	<Card.Footer class="flex-col gap-2 text-sm">
	</Card.Footer>
</Card.Root>