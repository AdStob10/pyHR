<script lang="ts">
	import type { UserWithRole } from '$lib/types';
    import { FilePenLine, Files, LogOut, Settings, UserCog, Users } from '@lucide/svelte';

    let { user } : {user: UserWithRole} = $props()
</script>



    <div class="flex flex-col gap-6 mt-3 px-2">
        <!-- flex flex-col items-center gap-4 px-2 py-4-->
        <div class="bg-primary p-2 text-foreground group flex shrink-0 items-center justify-center gap-2 rounded-full text-base md:text-lg font-semibold">
            <a
            href="/"
            class="hover:text-muted-foreground px-2.5"
            >
            PyHR
            </a>
        </div>
        <nav class="grid gap-6 text-lg font-medium">
            <a
            href="/requests"
            class="text-muted-foreground hover:text-foreground flex items-center gap-4 px-2.5"
        >
            <Files class="h-5 w-5"/>
            Wnioski urlopowe
        </a>
        </nav>
        {#if user.role.name == "MANAGER"}
           <nav class="grid gap-6 text-lg font-medium">
            <a
            href="/subordinates/requests"
                class="text-muted-foreground hover:text-foreground flex items-center gap-4 px-2.5"
            >
                <FilePenLine class="h-5 w-5"/>
                Wnioski pracowników
            </a>
            </nav>   
            <nav class="grid gap-6 text-lg font-medium">
            <a
            href="/subordinates"
                class="text-muted-foreground hover:text-foreground flex items-center gap-4 px-2.5"
            >
                <Users  class="h-5 w-5"/>
                Pracownicy
            </a>
            </nav>   
         
        {/if}
        <nav class="grid gap-6 text-lg font-medium">
            <a
            href={`/users/${user.id}`}
            class="text-muted-foreground hover:text-foreground flex items-center gap-4 px-2.5"
        >
            <UserCog class="h-5 w-5"/>
            Moje konto
        </a>
        </nav>
    </div>
    <nav class="mt-auto flex flex-col items-center gap-4 px-2 sm:py-5 text-sm">
            <a
              href="/signout"
              data-sveltekit-reload
              class="text-muted-foreground hover:text-foreground flex  items-center justify-center gap-4 rounded-lg transition-colors"
            >
            <LogOut class="w-5 h-5"/>
              Wyloguj się 
            </a>
    </nav>
