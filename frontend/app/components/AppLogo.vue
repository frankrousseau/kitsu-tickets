<template>
  <svg
    width="200"
    height="200"
    viewBox="0 0 200 200"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <defs>
      <mask id="ticket-mask">
        <rect width="200" height="200" fill="white" />
        <!-- Left side perforations -->
        <circle cx="20" cy="80" r="8" fill="black" />
        <circle cx="20" cy="120" r="8" fill="black" />
        <!-- Right side perforations -->
        <circle cx="180" cy="80" r="8" fill="black" />
        <circle cx="180" cy="120" r="8" fill="black" />
      </mask>
    </defs>
    <!-- Ticket body -->
    <rect
      x="20"
      y="40"
      width="160"
      height="120"
      rx="8"
      fill="currentColor"
      mask="url(#ticket-mask)"
    />
    <!-- Ticket content -->
    <rect
      x="50"
      y="70"
      width="100"
      height="12"
      rx="2"
      fill="var(--ui-background)"
      opacity="0.5"
    />
    <line
      x1="50"
      y1="100"
      x2="150"
      y2="100"
      stroke="var(--ui-background)"
      stroke-width="2"
      opacity="0.5"
    />
    <line
      x1="50"
      y1="120"
      x2="130"
      y2="120"
      stroke="var(--ui-background)"
      stroke-width="2"
      opacity="0.5"
    />
  </svg>
</template>
