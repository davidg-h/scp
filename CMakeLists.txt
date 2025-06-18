cmake_minimum_required(VERSION 3.15)
project(RemoteCli LANGUAGES CXX)

# ----------------------------
# 📦 Set SDK Root Path (EDIT THIS)
# ----------------------------
# 👉 User should set this to where the official SDK is extracted
set(CRSDK_SDK_ZIP_DIR "./test/SDK/CrSDK_Win64")  # <-- 🔧 Adjust this
set(CRSDK_ROOT "${CRSDK_SDK_ZIP_DIR}" CACHE PATH "Path to extracted Sony SDK")


# Verify path exists
if (NOT EXISTS "${CRSDK_ROOT}/app")
    message(FATAL_ERROR "❌ SDK folder not found! Please download and unzip it into: ${CRSDK_ROOT}")
endif()

# ----------------------------
# 📁 Copy SDK Files (optional)
# ----------------------------
# Optionally copy SDK folders locally if needed (run once)
file(COPY "${CRSDK_ROOT}/app" DESTINATION "${CMAKE_SOURCE_DIR}")
file(COPY "${CRSDK_ROOT}/external" DESTINATION "${CMAKE_SOURCE_DIR}")

# ----------------------------
# 🧠 Gather Source Files
# ----------------------------
file(GLOB_RECURSE APP_SRCS CONFIGURE_DEPENDS
    "${CMAKE_SOURCE_DIR}/app/*.cpp"
    "${CMAKE_SOURCE_DIR}/app/*.h"
)

add_executable(RemoteCli ${APP_SRCS})

# ----------------------------
# 🔧 C++17 and Unicode
# ----------------------------
set_target_properties(RemoteCli PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)
target_compile_definitions(RemoteCli PRIVATE UNICODE _UNICODE) # activate Unicode for Windows

# ----------------------------
# 📁 Include Directories
# ----------------------------
target_include_directories(RemoteCli PRIVATE
    "${CMAKE_SOURCE_DIR}/app"
    "${CMAKE_SOURCE_DIR}/app/CRSDK"
    "${CMAKE_SOURCE_DIR}/external/opencv/include"
)

# ----------------------------
# 🔗 Link Libraries
# ----------------------------

# Link Cr_Core.lib
find_library(CR_CORE_LIB Cr_Core
    PATHS "${CMAKE_SOURCE_DIR}/external/crsdk"
    REQUIRED
)

# Link OpenCV (Debug/Release)
if (MSVC)
    target_link_libraries(RemoteCli PRIVATE
        ${CR_CORE_LIB}
        $<$<CONFIG:Debug>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Debug/lib/opencv_core480d.lib>
        $<$<CONFIG:Debug>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Debug/lib/opencv_highgui480d.lib>
        $<$<CONFIG:Debug>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Debug/lib/opencv_imgcodecs480d.lib>
        $<$<CONFIG:Debug>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Debug/lib/opencv_imgproc480d.lib>
        $<$<CONFIG:Release>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Release/lib/opencv_core480.lib>
        $<$<CONFIG:Release>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Release/lib/opencv_highgui480.lib>
        $<$<CONFIG:Release>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Release/lib/opencv_imgcodecs480.lib>
        $<$<CONFIG:Release>:${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/Release/lib/opencv_imgproc480.lib>
    )
endif()

# ----------------------------
# 📤 Copy DLLs After Build
# ----------------------------
if (WIN32)
    # Copy CrSDK DLLs
    add_custom_command(TARGET RemoteCli POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E echo ""
        COMMAND ${CMAKE_COMMAND} -E echo "Copying CrSDK DLLs..."
        COMMAND ${CMAKE_COMMAND} -E copy_directory
            "${CMAKE_SOURCE_DIR}/external/crsdk"
            "$<TARGET_FILE_DIR:RemoteCli>"
    )

    # Copy correct OpenCV DLLs based on current config
    add_custom_command(TARGET RemoteCli POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E echo ""
        COMMAND ${CMAKE_COMMAND} -E echo "Copying OpenCV DLLs for $<CONFIG> build"
        COMMAND ${CMAKE_COMMAND} -E copy_directory
            "${CMAKE_SOURCE_DIR}/external/opencv/Windows/x86_64/$<CONFIG>/bin"
            "$<TARGET_FILE_DIR:RemoteCli>"
    )
endif()
# TODO add bindings part and switch from executeable to pyd