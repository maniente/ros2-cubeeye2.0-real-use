#include <sstream>
#include <thread>
#include <signal.h>

#include <rclcpp/rclcpp.hpp>
#include <rclcpp/logger.hpp>
#include <rclcpp_action/rclcpp_action.hpp>

#include "CubeEyeSink.h"
#include "CubeEyeCamera.h"
#include "CubeEyeIntensityPointCloudFrame.h"

#include "ICubeModelParameter.h"

static ModelParameter::Descriptor descriptors[] = {
    { "amplitude_threshold_max", "amplitude threshold max", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 65535 },
    { "amplitude_threshold_min", "amplitude threshold min", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 0 },
    { "auto_exposure", "auto exposure on/off", rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 0, 0, 1 },
    { "depth_range_min", "depth range min", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 150 },
    { "depth_range_max", "depth range max", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 65535 },
    { "flying_pixel_remove_filter", "flying pixel removal filter on/off", rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 0, 0, 1},
    { "flying_pixel_remove_threshold", "flying pixel removal filter treshold", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 3000},
    { "framerate", "framerate", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U8, 5, 15, 5, 15},
    { "integration_time", "integration time (depends on auto_exposure)", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 2000, 1, 1000 },
    { "median_filter", "median filter",rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 1, 1, 0 },
    { "noise_removal_threshold", "noise removal threshold", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 700},
    { "outlier_remove_filter", "outlier removal filter on/off", rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 0, 0, 1},
    { "phase_noise_filter", "outlier removal filter on/off", rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 0, 0, 0},
    { "scattering_filter", "scattering removal filter on/off", rcl_interfaces::msg::ParameterType::PARAMETER_BOOL, meere::sensor::DataType::Boolean, 0, 0, 0, 0},
    { "scattering_filter_threshold", "scattering removal threshold", rcl_interfaces::msg::ParameterType::PARAMETER_INTEGER, meere::sensor::DataType::U16, 0, 65535, 1, 700},
};

ICubeModelParameter::ICubeModelParameter(meere::sensor::sptr_camera camera) : ModelParameter(camera) {
    build(descriptors, sizeof(descriptors) / sizeof(ModelParameter::Descriptor));
}
