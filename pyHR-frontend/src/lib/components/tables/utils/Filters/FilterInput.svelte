<script lang="ts">
	import { Input } from "$lib/components/ui/input";

type FilterInputProps = {
    value: unknown,
    label: string,
    className?: string
}

let { value = $bindable(), label, className }: FilterInputProps = $props()

</script>

<div class={["flex-col justify-items-center gap-2", className]}>
    <h4 class="text-muted-foreground mb-2">{label}</h4>
    <Input bind:value />
</div>