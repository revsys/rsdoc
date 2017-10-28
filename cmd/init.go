package cmd

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/tcnksm/go-input"
)

const ConfigFilename = ".rsdoc.json"

type RsdocConfig struct {
	Docpath string `json:"docpath"`
	Version string `json:"version"`
	Token   string `json:"token"`
}

func checkError(err error) {
	if err != nil {
		fmt.Println("ERROR:", err)
		os.Exit(1)
	}
}

func generateEmpty(verbose bool) {
	if verbose {
		fmt.Printf("Generating empty %s file...\n", ConfigFilename)
	}

	empty := &RsdocConfig{}
	writeConfigFile(empty, verbose)
}

func writeConfigFile(config *RsdocConfig, verbose bool) {
	f, err := os.OpenFile(ConfigFilename, os.O_WRONLY|os.O_CREATE, 0644)
	checkError(err)
	configM, err := json.MarshalIndent(config, "", "    ")
	configString := string(configM)

	if verbose {
		fmt.Printf("Generated JSON Config file '%s':\n", ConfigFilename)
		fmt.Println(configString)
	}

	f.WriteString(string(configM))
	f.Close()
}

// initCmd represents the init command
var initCmd = &cobra.Command{
	Use:   "init",
	Short: "Configure a new set of docs",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		verbose, _ := cmd.Flags().GetBool("verbose")
		empty, _ := cmd.Flags().GetBool("empty")

		// See if our file already exists
		if _, err := os.Stat(ConfigFilename); !os.IsNotExist(err) {
			fmt.Printf("ERROR: %s already exists in this directory, exiting\n", ConfigFilename)
			os.Exit(1)
		}

		// Should we just make an empty one?
		if empty {
			generateEmpty(verbose)
			os.Exit(0)
		}

		// Get user input for our config values
		fmt.Printf("Initializing './%s' settings, please provide the following information:\n\n", ConfigFilename)

		ui := &input.UI{
			Writer: os.Stdout,
			Reader: os.Stdin,
		}

		doc_query := "What is the docpath?"
		docpath, err := ui.Ask(doc_query, &input.Options{
			Default:  "",
			Required: true,
			Loop:     true,
		})
		checkError(err)

		version_query := "What is the version?"
		version, err := ui.Ask(version_query, &input.Options{
			Default:  "v1",
			Required: true,
			Loop:     true,
		})
		checkError(err)

		token_query := "What is DocSet Token?"
		token, err := ui.Ask(token_query, &input.Options{
			Default:  "",
			Required: true,
			Loop:     true,
		})
		checkError(err)

		// Populate our config and write it out
		config := &RsdocConfig{
			Docpath: docpath,
			Version: version,
			Token:   token,
		}

		writeConfigFile(config, verbose)
	},
}

func init() {
	RootCmd.AddCommand(initCmd)
	initCmd.Flags().BoolP("empty", "e", false, "Create empty settings file")
}
