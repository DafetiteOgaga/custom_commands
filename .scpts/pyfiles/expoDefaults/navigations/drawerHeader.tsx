import React, {useState} from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';
import { Ionicons } from '@expo/vector-icons';
import { useCurrColorMode } from '@/constants/Colors';

const DASHBOARD_HEADER_HEIGHT = 220;
const CustomDrawerHeader = (props: any) => {
    const { userData, isDark } = props; // Make sure userData is passed as a prop
	const deviceColorScheme = useCurrColorMode()
	// const [scrollOffset, setScrollOffset] = useState(0);
	// const isHalfHeight = scrollOffset > DASHBOARD_HEADER_HEIGHT / 2;
	
    return (
        <DrawerContentScrollView {...props}>
            {/* Custom Header/Profile Section */}
            <View style={headerStyles.mainContainer}>
                <View
				style={headerStyles.contentContainer}
				>
                    <View style={[headerStyles.profileCircle, {backgroundColor: deviceColorScheme.dkb,}]}>
                        <Text style={headerStyles.profileInitial}>{userData.supervisor[0]}</Text>
                    </View>
                    <Text style={[headerStyles.namesText, { color: isDark ? "#FFFFFF" : "#1A202C" }]}>
                        {userData.supervisor}
                    </Text>
                    <View style={[headerStyles.roleTag,
						{backgroundColor: deviceColorScheme.dkrb,}
						]}>
                        <Text style={[headerStyles.roleText]}>{userData.role}</Text>
                    </View>
                    <View style={headerStyles.deliveries}>
                        <Ionicons name={'cube-outline'} size={15} color={'#fff'} />
                        <Text style={headerStyles.deliveriesText}>Deliveries: {userData.deliveries}</Text>
                    </View>
                </View>
            </View>
			<View style={headerStyles.line} />

            {/* Drawer Items */}
            <DrawerItemList {...props} />
        </DrawerContentScrollView>
    );
};
export { CustomDrawerHeader };

const headerStyles = StyleSheet.create({
	mainContainer: {
		flex: 1,
		// flexDirection: 'row',
		// paddingBottom: 30,
		
		// justifyContent: "center",
	},
	line: {
		height: 1,
		backgroundColor: "grey",
		marginVertical: 25
	},
	contentContainer: {
		paddingLeft: 15,
		// flexDirection: 'row',
		// gap: 10
	},
	profileCircle: {
		width: 50,
		height: 50,
		borderRadius: 50,
		// backgroundColor: deviceColorScheme.ltb,
		justifyContent: "center",
		alignItems: "center",
		// elevation: 6,
	},
	profileInitial: {
		fontSize: 30,
		fontWeight: "bold",
		color: "#FFFFFF",
	},
	namesText: {
		// textAlign: "center",
		marginTop: 5,
		fontSize: 22,
		fontWeight: "bold",
	},
	roleTag: {
		marginTop: 5,
		paddingVertical: 4,
		paddingHorizontal: 10,
		borderRadius: 8,
		alignSelf: "flex-start",
		// width: 100,
		// backgroundColor: deviceColorScheme.ltb,
		// height: 24,
	},
	roleText: {
		// display: "flex",
		fontSize: 14,
		// textAlign: "center",
		fontWeight: "600",
		color: '#fff'
	},
	deliveries: {
		flexDirection: "row",
		paddingTop: 5,
		alignItems: "center",
		// justifyContent: "center",
		// paddingTop: 5,
		// backgroundColor: "#2e6e39"
	},
	deliveriesText: {
		fontSize: 15,
		color: "#fff",
		fontStyle: "italic",
	},
})
