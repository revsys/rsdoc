package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

var cfgFile string

// RootCmd represents the base command when called without any subcommands
var RootCmd = &cobra.Command{
	Use:   "rsdoc",
	Short: "docs.revsys.com command line utility",
	Long:  `Manage and upload REVSYS documentation located at docs.revsys.com`,
}

// Execute adds all child commands to the root command and sets flags appropriately.
// This is called by main.main(). It only needs to happen once to the rootCmd.
func Execute() {
	if err := RootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}

func init() {
	cobra.OnInitialize(initConfig)

	// Here you will define your flags and configuration settings.
	// Cobra supports persistent flags, which, if defined here,
	// will be global for your application.
	RootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file (default is .rsdoc.json)")
	RootCmd.PersistentFlags().BoolP("verbose", "v", false, "Turn on verbose output")
	RootCmd.PersistentFlags().StringP("path", "p", "", "DocSet URL Path")
	RootCmd.PersistentFlags().StringP("version", "", "v1", "Version of the DocSet to use")
	RootCmd.PersistentFlags().StringP("token", "t", "", "DocSet Token to use")
}

// initConfig reads in config file and ENV variables if set.
func initConfig() {
	viper.SetConfigType("json")

	if cfgFile != "" {
		// Use config file from the flag.
		viper.SetConfigFile(cfgFile)
	} else {
		viper.AddConfigPath(".")
		viper.SetConfigName(".rsdoc")
	}

	// Pull in some environment or config files
	viper.BindEnv("docpath", "RSDOC_DOCPATH")
	viper.BindEnv("version", "RSDOC_VERSION")
	viper.BindEnv("token", "RSDOC_TOKEN")

	viper.AutomaticEnv() // read in environment variables that match

	viper.SetDefault("cookiecutter-repo-url", "https://github.com/revsys/revsys-doc-cookiecutter")
	viper.SetDefault("base-docs-url", "https://docs.revsys.com")

	// Read in our configuration file
	err := viper.ReadInConfig()

	if err != nil {
		fmt.Println("Error reading config file")
		panic(err)
	}
}
