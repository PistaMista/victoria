<!-- Must support both a pure list view (items in a column) and a flex-wrap layout with cards -->
<!-- There should be an option to either include or not include a back button -->

<!-- This is the pure list view -->
<div class="flex flex-col w-full h-full">
    <div class="p-1 bg-slate-400 flex flex-col md:flex-row">
        <slot name="header"/>
    </div>

    <div class="flex flex-col grow min-h-0 bg-slate-300 overflow-y-scroll">
        <slot name="items"/>
    </div>
</div>