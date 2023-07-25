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

