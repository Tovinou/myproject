#include <iostream>
#include <vector>
#include <string>
#include <yaml-cpp/yaml.h>

int main() {
    try {
        // Ladda YAML-filen
        YAML::Node config = YAML::LoadFile("parser.yaml");

        // Hämta data
        std::string name = config["name"].as<std::string>();
        int age = config["age"].as<int>();
        std::vector<std::string> items;

        for (const auto& item : config["items"]) {
            items.push_back(item.as<std::string>());
        }

        bool debug = config["settings"]["debug"].as<bool>();
        int timeout = config["settings"]["timeout"].as<int>();

        // Skriv ut data
        std::cout << "Name: " << name << std::endl;
        std::cout << "Age: " << age << std::endl;
        std::cout << "Items:" << std::endl;
        for (const auto& item : items) {
            std::cout << "- " << item << std::endl;
        }
        std::cout << "Debug: " << (debug ? "true" : "false") << std::endl;
        std::cout << "Timeout: " << timeout << std::endl;

    } catch (const YAML::Exception& e) {
        std::cerr << "YAML Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
