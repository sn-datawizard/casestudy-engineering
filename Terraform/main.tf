# Azure provider configuration
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    } 
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  features {}
}


# Create a resource group
resource "azurerm_resource_group" "amazingetl" {
  name     = "rg-amazingetl"
  location = "Germany West Central"
}


# Create a virtual network
resource "azurerm_virtual_network" "amazingetl_network" {
  name                = "vnet-amazingetl"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.amazingetl.location
  resource_group_name = azurerm_resource_group.amazingetl.name
}


# Create storage account and data lake gen2
resource "azurerm_storage_account" "amazingetl_storageaccount" {
  name                     = "storageacc1amazingetl"
  resource_group_name      = azurerm_resource_group.amazingetl.name
  location                 = azurerm_resource_group.amazingetl.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  is_hns_enabled           = "true"
}

resource "azurerm_storage_data_lake_gen2_filesystem" "amazingetl-datalake-bronze" {
  name               = "bronze-dlscontainer-amazingetl"
  storage_account_id = azurerm_storage_account.amazingetl_storageaccount.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "amazingetl-datalake-silver" {
  name               = "silver-dlscontainer-amazingetl"
  storage_account_id = azurerm_storage_account.amazingetl_storageaccount.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "amazingetl-datalake-gold" {
  name               = "gold-dlscontainer-amazingetl"
  storage_account_id = azurerm_storage_account.amazingetl_storageaccount.id
}


# Create Azure Data Factory service and linked service to datalake
resource "azurerm_data_factory" "amazingetl-datafactory" {
  name                = "df-amazingetl"
  location            = azurerm_resource_group.amazingetl.location
  resource_group_name = azurerm_resource_group.amazingetl.name
}

resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "amazingetl-linkedservice-bronze" {
  name                  = "ls-bronze-amazingetl"
  data_factory_id       = azurerm_data_factory.amazingetl-datafactory.id
  storage_account_key   = azurerm_storage_data_lake_gen2_filesystem.amazingetl-datalake-bronze.storage_account_id
  url                   = "https://datalakestoragegen2"
}

resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "amazingetl-linkedservice-silver" {
  name                  = "ls-silver-amazingetl"
  data_factory_id       = azurerm_data_factory.amazingetl-datafactory.id
  storage_account_key   = azurerm_storage_data_lake_gen2_filesystem.amazingetl-datalake-silver.storage_account_id
  url                   = "https://datalakestoragegen2"
}

resource "azurerm_data_factory_linked_service_data_lake_storage_gen2" "amazingetl-linkedservice-gold" {
  name                  = "ls-gold-amazingetl"
  data_factory_id       = azurerm_data_factory.amazingetl-datafactory.id
  storage_account_key   = azurerm_storage_data_lake_gen2_filesystem.amazingetl-datalake-gold.storage_account_id
  url                   = "https://datalakestoragegen2"
}
