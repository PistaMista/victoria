<script>
    import { Input, Button, Label } from "flowbite-svelte";
</script>

<div class="flex flex-col absolute inset-0">
    <div class="grow flex justify-center items-center">
        LOGO GOES HERE
    </div>
    <div class="flex justify-center m-2">
        <div class="flex shrink flex-col justify-start max-w-[10cm] w-1/2 h-1/3">
            <div class="flex justify-center">
                <h1 class="font-bold antialiased">Welcome back!</h1>
            </div>
            <div>
                <Label for="username" class="mb-2">Username</Label>
                <Input type="text" id="username" required/>
            </div>
            <div class="mt-2">
                <Label for="password" class="mb-2">Password</Label>
                <Input type="password" id="password" required/>
            </div>
            <div class="mt-2 flex">
                <Button class="grow">Log in</Button>
            </div>
            <div class="mt-1 text-xs flex justify-center">
                <span>Not registered? <a href="/register">Register here.</a></span>
            </div>
        </div>
    </div>
    <div class="grow"/>
</div>