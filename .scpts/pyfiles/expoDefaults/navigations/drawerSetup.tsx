import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Ionicons } from '@expo/vector-icons';
import { Colors, useCurrColorMode } from '../constants/Colors';
import { useNavigation, usePathname, useRouter } from 'expo-router';
import React from 'react';
import { screenConfig } from '@/myConfig/navigation'
import { CustomDrawerHeader } from './drawerHeader';
// import { useCurrColorMode } from '@/constants/Colors';

const userData = {
	state: "Lagos",
	location: "Ikeja",
	role: "Technician",
	supervisor: "John Doe",
	supervisorLink: "https://example.com/supervisor",
	helpDeskLink: "https://example.com/helpdesk",
	email: "johndoe@example.com",
	deliveries: 25,
	phone: "+234 812 345 6789",
	secondPhone: "+234 909 876 5432",
	region: "South-West",
	pendingFaults: 3,
};

export default function DrawerNavigator() {
	// const isDrawerOpen = useDrawerStatus();
	const colorScheme = useColorScheme();
	const deviceColorScheme = useCurrColorMode();
	let path:string|null = usePathname();
	const navigation: any|undefined = useNavigation();
	const [,titleKey] = path?.split('/')
	console.log({titleKey})
	return (
		<Drawer
		drawerContent={(props) => <CustomDrawerHeader {...props} userData={userData} isDark={colorScheme === 'dark'} />}
		screenOptions={{
			headerShown: true,
			drawerActiveBackgroundColor: colorScheme==='dark'?'#242f2f':'#dbd0d0',
			drawerActiveTintColor: colorScheme==='dark'?'#dfdfdf':'#464646',
			drawerInactiveTintColor: colorScheme==='dark'?'#9f9f9f':'#606060',
			headerSearchBarOptions: {
				placeholder: 'Search',
				onChangeText: (e) => console.log(e.nativeEvent.text),
			},
			headerStyle: {
				backgroundColor: deviceColorScheme.background,
				// You can add more custom styling here
			},
			headerTitleStyle: {
				fontWeight: 'bold',
				// You can add more custom styling here
			},
			// headerTitleAlign: 'center',
			// You can add more custom styling here
			drawerStyle: {
				backgroundColor: deviceColorScheme.vdrkb, // Background color
				width: 250, // Set drawer width
				// padding: 15, // Add padding inside drawer
				paddingTop: 20,
				borderTopRightRadius: 20, // Rounded corners on the top
				borderBottomRightRadius: 20, // Rounded corners on the bottom
			},
			drawerLabelStyle: {
				fontSize: 16, // Customize label size
				fontWeight: 'bold',
				// marginLeft: 10, // Add spacing to the left
			},
		}}
		>
			<Drawer.Screen
				name="(tabs)"
				options={({navigation})=>({
					title: screenConfig['index'].title,
					headerTitle: titleKey?`${screenConfig[titleKey]?.title}`:'Home Title',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['index'].icon} size={size} color={focused? color : color} />
					)
				})}
				listeners={{
					drawerItemPress: (e) => {
						e.preventDefault();
						navigation.navigate('(tabs)', { screen: 'index' });
					}
				}}
			/>
			<Drawer.Screen
				name="testcomp"
				options={{
					title: screenConfig['testcomp'].title,
					headerTitle: 'Test Component Title',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['testcomp'].icon} size={size} color={focused? color : color} />
					)
				}}
			/>
			<Drawer.Screen
				name="login"
				options={{
					title: screenConfig['login'].title,
					headerTitle: 'Login',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['login'].icon} size={size} color={focused? color : color} />
					)
				}}
			/>
			<Drawer.Screen
				name="chatroom"
				options={{
					title: screenConfig['chatroom'].title,
					headerTitle: 'ChatRoom',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['chatroom'].icon} size={size} color={focused? color : color} />
					)
				}}
			/>
			<Drawer.Screen
				name="profile"
				options={{
					title: screenConfig['profile'].title,
					headerTitle: 'Profile',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['profile'].icon} size={size} color={focused? color : color} />
					)
				}}
			/>
			<Drawer.Screen
				name="settings"
				options={{
					title: screenConfig['settings'].title,
					headerTitle: 'Settings',
					drawerIcon: ({focused, color, size}) => (
						<Ionicons name={screenConfig['settings'].icon} size={size} color={focused? color : color} />
					)
				}}
			/>
			<Drawer.Screen
				name="+not-found"
				options={{
					drawerItemStyle: { height: 0 },  // This hides the item from drawer
				}}
			/>
		</Drawer>
	);
}