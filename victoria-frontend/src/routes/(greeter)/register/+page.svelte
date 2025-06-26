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
                <h1 class="font-bold antialiased">User registration</h1>
            </div>
            <div>
                <Label for="username" class="mb-2">Username</Label>
                <Input type="text" id="username" required/>
            </div>
            <div class="mt-2">
                <Label for="password" class="mb-2">Password</Label>
                <Input type="password" id="password" required/>
            </div>
            <div class="mt-2">
                <Label for="password-confirm" class="mb-2">Confirm password</Label>
                <Input type="password" id="password-confirm" required/>
            </div>
            <div class="mt-2 flex">
                <Button class="grow">Register</Button>
            </div>
        </div>
    </div>
    <div class="grow"/>
</div>