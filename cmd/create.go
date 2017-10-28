package cmd

import (
	"fmt"
	"log"
	"os"
	"os/exec"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// createCmd represents the create command
var createCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new set of docs with cookiecutter",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		// Make sure cookiecutter is installed
		path, err := exec.LookPath("cookiecutter")
		if err != nil {
			log.Fatal("'cookiecutter' not found in your path, please install it with 'pip install cookiecutter'")
		}

		url := viper.GetString("cookiecutter-repo-url")
		fmt.Printf("Creating new initial doc set from '%s'...\n", url)
		exec_command(path, url)
	},
}

func init() {
	RootCmd.AddCommand(createCmd)

	createCmd.Flags().StringP("cookiecutter-repo-url", "", "URL", "Cookiecutter repo to use")
	viper.SetDefault("cookiecutter-repo-url", "https://github.com/revsys/revsys-doc-cookiecutter")
	viper.BindPFlag("cookiecutter-repo-url", createCmd.Flags().Lookup("cookiecutter-repo-url"))

}

func exec_command(program string, args ...string) {
	cmd := exec.Command(program, args...)
	cmd.Stdin = os.Stdin
	cmd.Stderr = os.Stderr
	cmd.Stdout = os.Stdout
	err := cmd.Run()

	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
