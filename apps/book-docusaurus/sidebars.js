/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '📖 Introduction',
    },
    {
      type: 'category',
      label: '🤖 Chapter 1: Introduction to Physical AI',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'chapter1-intro/introduction',
          label: '1.1 Physical AI Fundamentals',
        },
        {
          type: 'doc',
          id: 'chapter1-intro/components',
          label: '1.2 Key Components',
        },
      ],
    },
    {
      type: 'category',
      label: '🔧 Chapter 2: ROS 2 - The Robotic Nervous System',
      collapsible: true,
      collapsed: false,
      items: [
        {
          type: 'doc',
          id: 'chapter2-ros2/ros2-nervous-system',
          label: '2.1 ROS 2 Architecture',
        },
        {
          type: 'doc',
          id: 'chapter2-ros2/nodes-and-topics',
          label: '2.2 Nodes and Topics',
        },
        {
          type: 'doc',
          id: 'chapter2-ros2/services-and-actions',
          label: '2.3 Services and Actions',
        },
      ],
    },
    {
      type: 'category',
      label: '🌐 Chapter 3: Digital Twin Simulation',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter3-digital-twin/digital-twin-simulation',
          label: '3.1 Digital Twin Concepts',
        },
        {
          type: 'doc',
          id: 'chapter3-digital-twin/gazebo',
          label: '3.2 Gazebo Simulation',
        },
        {
          type: 'doc',
          id: 'chapter3-digital-twin/unity',
          label: '3.3 Unity Integration',
        },
      ],
    },
    {
      type: 'category',
      label: '🧠 Chapter 4: NVIDIA Isaac - The AI-Robot Brain',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter4-nvidia-isaac/nvidia-isaac-ai-brain',
          label: '4.1 Isaac Sim Overview',
        },
        {
          type: 'doc',
          id: 'chapter4-nvidia-isaac/perception',
          label: '4.2 AI Perception',
        },
      ],
    },
    {
      type: 'category',
      label: '👁️ Chapter 5: Vision-Language-Action Models',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter5-vla/vision-language-action',
          label: '5.1 VLA Fundamentals',
        },
      ],
    },
    {
      type: 'category',
      label: '🚶 Chapter 6: Humanoid Robotics Development',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter6-humanoid-robotics/humanoid-robot-dev',
          label: '6.1 Humanoid Kinematics',
        },
      ],
    },
    {
      type: 'category',
      label: '📚 Chapter 7: Building the AI-Native Textbook',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter7-ai-native-textbook/ai-native-textbook-build',
          label: '7.1 Architecture Overview',
        },
      ],
    },
    {
      type: 'category',
      label: '🌍 Chapter 8: Personalization, Translation & Subagents',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter8-personalization/personalization-translation',
          label: '8.1 Personalization Features',
        },
      ],
    },
    {
      type: 'category',
      label: '🎯 Chapter 9: Capstone Project',
      collapsible: true,
      collapsed: true,
      items: [
        {
          type: 'doc',
          id: 'chapter9-capstone/autonomous-humanoid-robot',
          label: '9.1 Project Overview',
        },
      ],
    },
  ],
};

module.exports = sidebars;