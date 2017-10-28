package cmd

import (
	"fmt"

	"github.com/spf13/cobra"
)

// groupCmd represents the group command
var groupCmd = &cobra.Command{
	Use:   "group",
	Short: "Manage user membership and create new doc groups",
	Long:  `Add `,
	Run: func(cmd *cobra.Command, args []string) {
		usage := cmd.UsageFunc()
		usage(cmd)
	},
}

// groupAddCmd
var groupAddCmd = &cobra.Command{
	Use:   "add",
	Short: "Add user to an existing group",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("group add called")
	},
}

// groupCreateCmd
var groupCreateCmd = &cobra.Command{
	Use:   "create",
	Short: "Create a new group",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("group create called")
	},
}

func init() {
	groupCmd.AddCommand(groupAddCmd, groupCreateCmd)
	RootCmd.AddCommand(groupCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// groupCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// groupCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
