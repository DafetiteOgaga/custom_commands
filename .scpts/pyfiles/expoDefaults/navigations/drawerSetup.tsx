import { Drawer } from 'expo-router/drawer';
import { useColorScheme } from '@/hooks/useColorScheme';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/Colors';
import { useNavigation, usePathname, useRouter } from 'expo-router';
import React from 'react';
import { screenConfig } from '@/myConfig/navigation'

export default function DrawerNavigator() {
	// const isDrawerOpen = useDrawerStatus();
	const colorScheme = useColorScheme();
	let path:string|null = usePathname();
	const navigation: any|undefined = useNavigation();
	const [,titleKey] = path?.split('/')
	return (
		<Drawer screenOptions={{
			headerShown: true,
			drawerActiveBackgroundColor: colorScheme==='dark'?'#242f2f':'#dbd0d0',
			drawerActiveTintColor: colorScheme==='dark'?'#dfdfdf':'#464646',
			drawerInactiveTintColor: colorScheme==='dark'?'#9f9f9f':'#606060',
			headerSearchBarOptions: {
				placeholder: 'Search',
				onChangeText: (e) => console.log(e.nativeEvent.text),
			},
			headerStyle: {
				backgroundColor: Colors[colorScheme?? 'light'].background,
				// You can add more custom styling here
			},
			headerTitleStyle: {
				fontWeight: 'bold',
				// You can add more custom styling here
			},
			// headerTitleAlign: 'center',
			// You can add more custom styling here
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
				name="+not-found"
				options={{
				drawerItemStyle: { height: 0 },  // This hides the item from drawer
				}}
			/>
		</Drawer>
	);
}