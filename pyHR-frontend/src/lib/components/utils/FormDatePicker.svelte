	
<script lang="ts">
  import CalendarIcon from "@lucide/svelte/icons/calendar";
  import {
    type DateValue,
    DateFormatter,
    getLocalTimeZone,
	parseDate,
  } from "@internationalized/date";
  import { cn } from "$lib/utils.js";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Calendar } from "$lib/components/ui/calendar/index.js";
  import * as Popover from "$lib/components/ui/popover/index.js";

  const df = new DateFormatter("pl-PL", {
    dateStyle: "medium",
  });
 
    type FormDatePickerProps = {
    value: string | undefined
  }

    let {value = $bindable()}: FormDatePickerProps = $props();
    let open = $state(false)
 
    const dateValueFromString = (date: string | undefined) => {
        return date ? parseDate(date) : undefined
    }
</script>
 
<Popover.Root>
  <Popover.Trigger>
    {#snippet child({ props })}
      <Button
        variant="outline"
        class={cn(
          "w-[280px] justify-start text-left font-normal",
          !value && "text-muted-foreground"
        )}
        {...props}
      >
        <CalendarIcon class="mr-2 size-4" />
        {value ? df.format(new Date(value)) : "Wybierz datę"}
      </Button>
    {/snippet}
  </Popover.Trigger>
  <Popover.Content class="w-auto p-0">
   <Calendar bind:value={
        () => dateValueFromString(value),
        (val) => {
            value = val?.toString()
        }
    } type="single" initialFocus />
  </Popover.Content>
</Popover.Root>

