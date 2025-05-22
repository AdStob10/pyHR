<script lang="ts">
 import CalendarIcon from "@lucide/svelte/icons/calendar";
 import type { DateRange } from "bits-ui";
 import {
  CalendarDate,
  DateFormatter,
  type DateValue,
  fromAbsolute,
  fromDate,
  getLocalTimeZone,

  parseDate

 } from "@internationalized/date";
 import { cn } from "$lib/utils.js";
 import { Button, buttonVariants } from "$lib/components/ui/button/index.js";
 import { RangeCalendar } from "$lib/components/ui/range-calendar/index.js";
 import * as Popover from "$lib/components/ui/popover/index.js";
	import { X } from "@lucide/svelte";

 const df = new DateFormatter("pl-PL", {
  dateStyle: "medium"
 });

  type RangeDatePickerProps = {
    start: string | undefined,
    end: string | undefined,
  }

    let {start = $bindable(), end = $bindable()}: RangeDatePickerProps = $props();
    let open = $state(false)
 
    const dateRangeFromDates = (start: string | undefined, end:string | undefined) => {
        return {
            start: start ? parseDate(start) : undefined,
            end: end ? parseDate(end) : undefined
        } as DateRange
    }
</script>
 
<div class="grid gap-2">
 <Popover.Root bind:open>
  <Popover.Trigger
   class={cn(
    buttonVariants({ variant: "outline" }),
    !start && !end && "text-muted-foreground"
   )}
  >
   <CalendarIcon class="mr-2 size-4" />
   {#if start}
    {#if end}
     {df.format(new Date(start))} - {df.format(new Date(end))}
    {:else}
     {df.format(new Date(start))}
    {/if}
   {:else}
    Wybierz zakres...
   {/if}
  </Popover.Trigger>
  <Popover.Content class="w-auto p-0" align="start">
    <div class="flex justify-end">
        <Button variant="ghost" onclick={() => open = false}>
            <X class="w-5 h-5"/>
        </Button>
    </div>
   <RangeCalendar
    bind:value={
        () => dateRangeFromDates(start, end),
        (val) => {
            start = val.start?.toString()
            end = val.end?.toString()
        }
    }
    numberOfMonths={2}
   />
  </Popover.Content>
 </Popover.Root>
</div>