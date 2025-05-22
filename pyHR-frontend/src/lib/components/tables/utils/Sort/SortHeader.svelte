	
<script lang="ts">
  import type { ComponentProps } from "svelte";
  import ArrowUpDownIcon from "@lucide/svelte/icons/arrow-up-down";
  import { Button } from "$lib/components/ui/button/index.js";
	import type { SortDirection } from "@tanstack/table-core";
	import { ArrowDownIcon, ArrowUpIcon } from "@lucide/svelte";
 
  type SortButtonProps = ComponentProps<typeof Button> & {
    label: string
    direction: SortDirection | false
  }
  let {label, direction, variant = "ghost", ...restProps }: SortButtonProps =
    $props();

  
</script>
 

<Button {variant} {...restProps} class="text-left ml-0 p-0 hover:bg-background-muted">
  {label}
  {#if direction == "asc"}
    <ArrowUpIcon class="ml-1" />
  {:else if direction == "desc"}
    <ArrowDownIcon class="ml-1" />
  {:else}
    <ArrowUpDownIcon class="ml-1" />
  {/if}
</Button>

