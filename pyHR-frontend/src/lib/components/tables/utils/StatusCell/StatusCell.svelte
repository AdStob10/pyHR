<script lang='ts'>
	import { vacationStatuses } from "$lib/utils/objects";


    let {statusId} = $props();
    const rowStatus = $derived(vacationStatuses.find(s => s.id == statusId))
    const Icon = $derived(rowStatus?.icon)
    // if (!rowStatus) {
    //     throw Error(`Missing status object for ${statusId}`)
    // }
</script>

<div class="flex max-w-3xs items-center">

    <Icon class="text-muted-foreground mr-2 h-4 w-4" />

    <span>{rowStatus?.name}</span>
</div>
