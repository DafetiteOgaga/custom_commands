import { Tabs } from 'expo-router';
import React from 'react';
import { Platform } from 'react-native';
import { HapticTab } from '@/components/HapticTab';
// import TabBarBackground from '@/components/ui/TabBarBackground';
import { Colors } from '@/constants/Colors';
import { useColorScheme } from '@/hooks/useColorScheme';
import { screenConfig } from '@/myConfig/navigation';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  const colorScheme = useColorScheme(); // 'light' | 'dark'
  return (
    <>
      <Tabs
        // options and styles for the tabs and the tab bar
        screenOptions={{
          headerShown: false, // hide the header
          tabBarActiveTintColor: Colors[colorScheme ?? 'light'].tint, // active tab text color
          tabBarButton: HapticTab,  // custom tab button component
          // tabBarBackground: TabBarBackground,
          // tab style
          tabBarStyle: Platform.select({
            ios: {
              // Use a transparent background on iOS to show the blur effect
              position: 'absolute',
            },
            default: { // Android and others
              backgroundColor: Colors[colorScheme ?? 'light'].background,
            },
          }),
        }}>
        <Tabs.Screen //home screen
          name="index" // screen name (navigation)
          options={{
            title: screenConfig.index.title, // tab title
            // tab icon and color
            tabBarIcon: ({ color }) => <Ionicons size={28} name={screenConfig.index.icon} color={color} />,
          }}
        />
        <Tabs.Screen // explore screen
          name="explore" // screen name (navigation)
          // initialParams={{ title: 'Explore Tab' }}
          options={{
            title: screenConfig.explore.title, // tab title
            // tab icon and color
            tabBarIcon: ({ color }) => <Ionicons size={28} name={screenConfig.explore.icon} color={color} />,
            tabBarBadge: 3, // show a badge on the tab
            tabBarBadgeStyle: { // badge style
              backgroundColor: '#1111e1',
            },
          }}
        />
        <Tabs.Screen // greet screen
          name="greet" // screen name (navigation)
          initialParams={{ // default parameter value
            message: 'Hello, Anon!\nFron default parameter value'
          }}
          options={{
            title: screenConfig.greet.title, // tab title
            // tab icon and color
            tabBarIcon: ({ color }) => <Ionicons size={28} name={screenConfig.greet.icon} color={color} />,
          }}
        />
      </Tabs>
    </>
  );
}
