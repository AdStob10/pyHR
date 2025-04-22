<script lang="ts">
    import '../../app.css';
    import logo from '$lib/assets/logo3.png';
    import AuthForm from '$lib/components/custom/AuthForm/AuthForm.svelte';

    let {data} = $props();
</script>

<div 
class="container  relative  min-h-screen flex-col items-center justify-center grid lg:grid-cols-2 lg:px-0">
    <div class="bg-muted/20 relative hidden h-full flex-col p-10 text-white lg:flex border-r-1">
      <!--  <div style="background-image:url({logo})" class="bg-primary h-full absolute inset-0 "></div>-->
        <img src={logo} class="bg-primary absolute h-full inset-0" alt="logo"/>
    </div>
    <div class="lg:p-8">
        <div class="mx-auto flex w-full flex-col justify-center space-y-6 sm:w-[350px]">
            <div class="flex flex-col space-y-2 text-center">
                <h1 class="text-2xl font-semibold tracking-tight">Zaloguj się</h1>
                <p class="text-muted-foreground text-sm">
                    Wprowadź nazwę użytkownika i hasło
                </p>
            </div>
            <AuthForm data={data.form} />
        </div>
    </div>


</div>