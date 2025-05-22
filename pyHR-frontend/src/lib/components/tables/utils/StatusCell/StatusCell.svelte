<script lang='ts'>
	import { vacationStatuses } from "$lib/utils/objects";


    let {statusId} = $props();
    const rowStatus = vacationStatuses.find(s => s.id == statusId)
    if (!rowStatus) {
        throw Error(`Missing status object for ${statusId}`)
    }

    const Icon = rowStatus.icon
</script>


<div class="flex w-[100px] items-center">
    <Icon class="text-muted-foreground mr-2 h-4 w-4" />
    <span>{rowStatus.name}</span>
</div>
