def create_build_gradle(namespace):
    file_name = "build.gradle.kts"
    file_content = f'''plugins {{
    id("com.android.library")
    id("org.jetbrains.kotlin.android")
    id("kotlin-android")
    id("kotlin-kapt")
    id("dagger.hilt.android.plugin")
}}

android {{
    namespace = "{namespace}"
    compileSdk = Versions.compileSdk

    flavorDimensions.add("environment")

    productFlavors {{
        create("production") {{
            dimension = "environment"
        }}
        create("staging") {{
            dimension = "environment"
        }}
        create("dev") {{
            dimension = "environment"
        }}
    }}

    defaultConfig {{
        minSdk = Versions.minSdk

        consumerProguardFiles("consumer-rules.pro")
    }}

    buildTypes {{
        release {{
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }}
    }}
    compileOptions {{
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }}
    kotlinOptions {{
        jvmTarget = "1.8"
    }}
    buildFeatures {{
        compose = true
    }}
    composeOptions {{
        kotlinCompilerExtensionVersion = Versions.composeCompilerVersion
    }}
}}

dependencies {{
    implementation(project(":core:base"))
    implementation(project(":core:common"))
    implementation(project(":core:design-system"))
    implementation(project(":core:ui"))
    implementation(project(":models"))

    implementation(Libs.AndroidX.coreKtx)
    implementation(Libs.AndroidX.composeUi)
    implementation(Libs.AndroidX.lifecycleRuntimeKtx)
    implementation(Libs.AndroidX.viewModelCompose)
    implementation(Libs.AndroidX.activityCompose)
    implementation(Libs.AndroidX.composeUiTooling)

    // Nav
    implementation(Libs.AndroidX.navigationCompose)
    implementation(Libs.Accompanist.navigationMaterial)

    // Material3
    implementation(Libs.AndroidX.material3)

    // Dagger hilt
    implementation(Libs.Hilt.hilt)
    implementation(Libs.AndroidX.viewModelCompose)
    implementation(Libs.AndroidX.hiltNavigation)
    kapt(Libs.Hilt.hiltAndroidCompiler)
    kapt(Libs.AndroidX.hiltCompiler)

    implementation(Libs.Accompanist.permissions)
    implementation(Libs.Coil.coilCompose)

}}
'''
    with open(file_name, "w") as file:
        file.write(file_content)

