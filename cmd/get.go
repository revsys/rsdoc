package cmd

import (
	"fmt"
	"log"
	"net/url"
	"path"
	"strings"

	"github.com/spf13/cobra"
	"github.com/spf13/viper"
)

// Get full DocSet URL
func GetDocSetURL() string {
	// Get base URL and parse it into a Path
	baseurl := viper.GetString("base-docs-url")
	docpath := viper.GetString("docpath")
	version := viper.GetString("version")

	u, err := url.Parse(baseurl)
	if err != nil {
		log.Fatal(err)
	}

	u.Path = path.Join(u.Path, docpath, version)

	full_url := u.String()
	if !strings.HasSuffix(full_url, "/") {
		s := []string{full_url, "/"}
		full_url = strings.Join(s, "")
	}

	return full_url
}

// getCmd represents the get command
var getCmd = &cobra.Command{
	Use:   "get",
	Short: "Retrieve information about this set of docs",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		usage := cmd.UsageFunc()
		usage(cmd)
	},
}

// getURLCmd
var getURLCmd = &cobra.Command{
	Use:   "url",
	Short: "Get the URL for this set of docs",
	Long:  ``,
	Run: func(cmd *cobra.Command, args []string) {
		full_url := GetDocSetURL()
		fmt.Println(full_url)
	},
}

func init() {
	getCmd.AddCommand(getURLCmd)
	RootCmd.AddCommand(getCmd)
}
