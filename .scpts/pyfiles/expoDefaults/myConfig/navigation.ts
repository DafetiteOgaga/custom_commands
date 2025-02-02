/**
 * centralize titles and icons for the navigations
 */

import { Ionicons } from '@expo/vector-icons';

type IconNameTYpe = keyof typeof Ionicons.glyphMap;
export const screenConfig: Record<string, { title: string; icon: IconNameTYpe }> = {
	index: {
		title: 'Home Tab/Drawer config',
		icon: 'home',
	},
	explore: {
		title: 'Explore Tab config',
		icon: 'paper-plane',
	},
	greet: {
		title: 'Greetings Tab config',
		icon: 'library',
	},
	testcomp: {
		title: 'Test Component Drawer config',
		icon: 'american-football',
	},
	// ... other screens
};
