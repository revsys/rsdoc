package cmd

import (
	"fmt"

	"github.com/skratchdot/open-golang/open"
	"github.com/spf13/cobra"
)

// openCmd represents the open command
var openCmd = &cobra.Command{
	Use:   "open",
	Short: "Open these docs in your browser",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		full_url := GetDocSetURL()
		fmt.Printf("opening %s\n", full_url)
		open.Run(full_url)
	},
}

func init() {
	RootCmd.AddCommand(openCmd)
}
