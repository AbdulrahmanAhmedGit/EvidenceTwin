export const brandAssets={
 full:{light:'/brand/evidencetwin-logo.svg',dark:'/brand/evidencetwin-logo-dark.svg',width:1277,height:298},
 icon:{light:'/brand/evidencetwin-icon.svg',dark:'/brand/evidencetwin-icon-dark.svg',width:317,height:339},
} as const
export const faviconAssets={
 light:{svg:brandAssets.icon.light,png:'/brand/favicon-32.png',png16:'/brand/favicon-16.png'},
 dark:{svg:brandAssets.icon.dark,png:'/brand/favicon-32-dark.png',png16:'/brand/favicon-16-dark.png'},
} as const
