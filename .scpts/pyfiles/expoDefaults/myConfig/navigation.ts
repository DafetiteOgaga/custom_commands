/**
 * centralize titles and icons for the navigations
 */

import { StyleSheet } from 'react-native';
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
	login: {
		title: 'Login',
		icon: 'log-in',
	},
	// ... other screens
};

export const generalstyles = StyleSheet.create({
    card: {
        padding: 16,
        borderRadius: 10,
        borderWidth: 1,
    },
    titleText: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    notFound: {
        fontSize: 20,
        fontWeight: 'bold',
        alignSelf: 'center',
        paddingTop: 100
    },
    headerFooter: {
        fontSize: 25,
        fontWeight: 'bold',
        alignSelf: 'center',
        padding: 10,
    },
    loading: {
        justifyContent: 'center',
        alignItems: 'center',
    },
    formContainer: {
        padding: 20,
        borderRadius: 10,
        marginBottom: 10,
        borderWidth: 1,
    },
    input: {
        borderWidth: 1,
        padding: 10,
        marginBottom: 10,
        borderRadius: 5,
    },
    errorContainer: {
        paddingTop: 100,
    },
    errorText: {
        fontSize: 25,
        fontWeight: 'bold',
        alignSelf: 'center',
        color: 'red',
        textAlign: 'center',
        // borderWidth: 1,
        paddingTop: 10,
    },
    imageContainer: {
        // width: 10
    },
    image: {
        width: 100,
        height: 40,
        resizeMode: 'contain',
    },
});

export const ScreenStyle = StyleSheet.create({
	allScreenContainer: {
        flex: 1,
        paddingHorizontal: 10,
    },
})
