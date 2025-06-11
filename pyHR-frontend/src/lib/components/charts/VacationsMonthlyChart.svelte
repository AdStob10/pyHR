<script lang="ts">
	import type { VacationInMonth } from "$lib/types";
	import { getLocalTimeZone, today } from "@internationalized/date";
	import * as Card from "../ui/card";
	import * as Chart from "../ui/chart";
    import { BarChart, Text, type ChartContextValue } from "layerchart";
	import { mapVacationMonthlyToChartData } from "$lib/utils/chart";
	import { cubicInOut } from "svelte/easing";


    let {data}: {data: VacationInMonth[]} = $props()
    const chartData =  mapVacationMonthlyToChartData(data)

    const chartConfig = {
        newDays: {
            label: "Nowy",
            color: "#60a5fa"
        },
        acceptedDays: {
            label: "Zaakceptowany",
            color: "#2563eb"
        },
        rejectedDays: {
            label: "Odrzucony",
            color: "#de3333"
        }
    } satisfies Chart.ChartConfig


    let context = $state<ChartContextValue>();
    const totalAcceptedDays = data.reduce((acc, curr) => acc + curr.acceptedDays, 0)
    const totalNewDays = data.reduce((acc, curr) => acc + curr.newDays, 0)
    const totalRejectedDays = data.reduce((acc, curr) => acc + curr.rejectedDays, 0)
</script>



<Card.Root class="flex flex-col">
	<Card.Header class="items-center">
		<Card.Title>Urlopy</Card.Title>
		<Card.Description>Rok {today(getLocalTimeZone()).year}</Card.Description>
	</Card.Header>
	<Card.Content class="flex-1">
		<Chart.Container config={chartConfig} class="mx-auto aspect-square max-h-[250px]">
			<Chart.Container config={chartConfig} class="min-h-[200px] w-full">
            <BarChart
                bind:context
                data={chartData}
                x="month"
                axis="x"
                seriesLayout="group"
                series={[
                {
                    key: "newDays",
                    label: chartConfig.newDays.label,
                    color: chartConfig.newDays.color
                },
                {
                    key: "acceptedDays",
                    label: chartConfig.acceptedDays.label,
                    color: chartConfig.acceptedDays.color
                },
                {
                    key: "rejectedDays",
                    label: chartConfig.rejectedDays.label,
                    color: chartConfig.rejectedDays.color
                }
                ]}
                props={{
					bars: {
						stroke: "none",
						strokeWidth: 0,
						rounded: "all",

						initialY: context?.height,
						initialHeight: 0,
						motion: {
							y: { type: "tween", duration: 500, easing: cubicInOut },
							height: { type: "tween", duration: 500, easing: cubicInOut },
						},
					},
                    }
                }
            >
            {#snippet tooltip()}
                <Chart.Tooltip indicator="line"/>
            {/snippet}
            </BarChart> 
            </Chart.Container>
		</Chart.Container>
	</Card.Content>
	<Card.Footer class="flex-col gap-2 text-sm">
        <div class="flex w-full items-center justify-center gap-3 text-sm">
             <div class="flex gap-1">
                <div class="flex items-center gap-2 font-medium leading-none">
                Dni niezaakceptowane:
                </div>
                <div class="text-muted-foreground flex items-center gap-2 leading-none">
                    {totalNewDays} dni
                </div>
			</div>
			<div class="flex gap-1">
                <div class="flex items-center gap-2 font-medium leading-none">
                Dni zaakceptowane:
                </div>
                <div class="text-muted-foreground flex items-center gap-2 leading-none">
                    {totalAcceptedDays} dni
                </div>
			</div>
            <div class="flex gap-1">
                <div class="flex items-center gap-2 font-medium leading-none">
                Dni odrzucone:
                </div>
                <div class="text-muted-foreground flex items-center gap-2 leading-none">
                    {totalRejectedDays} dni
                </div>
			</div>
            <div class="flex gap-1">
                <div class="flex items-center gap-2 font-medium leading-none">
                Suma:
                </div>
                <div class="text-muted-foreground flex items-center gap-2 leading-none">
                    {totalNewDays + totalAcceptedDays + totalRejectedDays} dni
                </div>
			</div>
		</div>
	</Card.Footer>
</Card.Root>