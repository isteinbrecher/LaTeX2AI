// -----------------------------------------------------------------------------
// MIT License
//
// Copyright (c) 2020-2026 Ivo Steinbrecher
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in
// all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.
// -----------------------------------------------------------------------------

/**
 * \brief File system functions testing.
 */


#include "IllustratorSDK.h"

#include "test_latex.h"

#include "testing_utility.h"

#include "l2a_file_system.h"
#include "l2a_latex.h"


/**
 *
 */
void TestLatexBase(L2A::TEST::UTIL::UnitTest& ut, const ai::FilePath& temp_directory)
{
    ai::FilePath test_directory = temp_directory;
    test_directory.AddComponent(ai::UnicodeString("latex_test_") + L2A::TEST::UTIL::test_string_unicode());
    L2A::UTIL::RemoveDirectoryAI(test_directory, false);
    L2A::UTIL::CreateDirectoryL2A(test_directory);

    ai::FilePath tex_file = test_directory;
    tex_file.AddComponent(ai::UnicodeString(L2A::TEST::UTIL::test_string_unicode() + "test.tex"));

    L2A::UTIL::WriteFileUTF8(
        tex_file, ai::UnicodeString(
                      "\\documentclass{article}\n\\usepackage[utf8]{inputenc}\n\\begin{document}Test\\end{document}"));

    // Compile the latex file
    ai::FilePath pdf_file;
    const auto compile_ok = L2A::LATEX::CompileLatexDocument(tex_file, pdf_file);
    ut.CompareInt(compile_ok, 1);
    ut.CompareInt(L2A::UTIL::IsFile(pdf_file), 1);
}

/**
 *
 */
void TestHeader(L2A::TEST::UTIL::UnitTest& ut, const ai::FilePath& temp_directory)
{
    ai::FilePath header_1 = temp_directory;
    header_1.AddComponent(ai::UnicodeString("header1.txt"));
    L2A::UTIL::WriteFileUTF8(header_1, ai::UnicodeString("header1\n\\input{ header2.txt }\nheader1"));

    ai::FilePath header_2 = temp_directory;
    header_2.AddComponent(ai::UnicodeString("header2.txt"));
    L2A::UTIL::WriteFileUTF8(header_2, ai::UnicodeString("header2\n\\input{% check that comments do nothing\n header3 "
                                                         "\n}\n\\input{header4}\n\n\\input{ header 5.txt }\nheader2"));

    ai::FilePath header_3 = temp_directory;
    header_3.AddComponent(ai::UnicodeString("header3"));
    L2A::UTIL::WriteFileUTF8(header_3, ai::UnicodeString("header3"));

    ai::FilePath header_4 = temp_directory;
    header_4.AddComponent(ai::UnicodeString("header4.tex"));
    L2A::UTIL::WriteFileUTF8(header_4, ai::UnicodeString("header4"));

    ai::FilePath header_5 = temp_directory;
    header_5.AddComponent(ai::UnicodeString("header 5.txt"));
    L2A::UTIL::WriteFileUTF8(header_5, ai::UnicodeString("header5"));

    const auto resolved_inputs = L2A::LATEX::GetHeaderWithIncludedInputs(header_1);
    const ai::UnicodeString reference_header("header1\nheader2\nheader3\nheader4\n\nheader5\nheader2\nheader1");
    ut.CompareStr(L2A::UTIL::StringStdToAi(resolved_inputs), reference_header);
}

/**
 *
 */
void TestStripComments(L2A::TEST::UTIL::UnitTest& ut)
{
    auto compare_strip_comments = [&](const ai::UnicodeString& input,
                                      const ai::UnicodeString& expected_whitespace_preserved,
                                      const ai::UnicodeString& expected_whitespace_removed)
    {
        const auto out_whitespace_preserved = L2A::UTIL::StringStdToAi(L2A::LATEX::StripLatexComments(
            L2A::UTIL::StringAiToStd(input), L2A::LATEX::LatexCommentStripMode::PreserveWhitespace));
        ut.CompareStr(out_whitespace_preserved, expected_whitespace_preserved);

        const auto out_whitespace_removed = L2A::UTIL::StringStdToAi(
            L2A::LATEX::StripLatexComments(L2A::UTIL::StringAiToStd(input), L2A::LATEX::LatexCommentStripMode::Remove));
        ut.CompareStr(out_whitespace_removed, expected_whitespace_removed);
    };

    // Standard test
    {
        const ai::UnicodeString input(
            "hello % comment\n"
            "100\\% correct % another\n"
            "% full line comment with % percent sign\n"
            "immediately following comment%\n"
            "\\input{a} % trailing\n"
            "%\n"
            "done");

        const ai::UnicodeString expected_whitespace_preserved(
            "hello          \n"
            "100\\% correct          \n"
            "                                       \n"
            "immediately following comment \n"
            "\\input{a}           \n"
            " \n"
            "done");

        const ai::UnicodeString expected_whitespace_removed(
            "hello \n"
            "100\\% correct \n"
            "\n"
            "immediately following comment\n"
            "\\input{a} \n"
            "\n"
            "done");

        compare_strip_comments(input, expected_whitespace_preserved, expected_whitespace_removed);
    }

    // Test with trailing whitespace
    {
        const ai::UnicodeString input(
            "hello % comment   \n"
            "done");

        const ai::UnicodeString expected_whitespace_preserved(
            "hello             \n"
            "done");

        const ai::UnicodeString expected_whitespace_removed(
            "hello \n"
            "done");

        compare_strip_comments(input, expected_whitespace_preserved, expected_whitespace_removed);
    }

    // Test with unicode and umlauts whitespace
    {
        const auto input = ai::UnicodeString(  //
            L2A::TEST::UTIL::test_string_unicode() + " % comment   \n" + L2A::TEST::UTIL::test_string_6_ +
            " % comment   \n" + "done");

        const auto expected_whitespace_preserved = ai::UnicodeString(  //
            L2A::TEST::UTIL::test_string_unicode() + "             \n" + L2A::TEST::UTIL::test_string_6_ +
            "             \n" + "done");

        const auto expected_whitespace_removed = ai::UnicodeString(  //
            L2A::TEST::UTIL::test_string_unicode() + " \n" + L2A::TEST::UTIL::test_string_6_ + " \n" + "done");

        compare_strip_comments(input, expected_whitespace_preserved, expected_whitespace_removed);
    }
}

/**
 *
 */
void L2A::TEST::TestLatex(L2A::TEST::UTIL::UnitTest& ut)
{
    // Set test name.
    ut.SetTestName(ai::UnicodeString("TestLatex"));

    // Store the working, so we can reset it at the end
    const auto old_cwd = std::filesystem::current_path();

    // Get the name of the temp directory and clear it.
    const auto temp_directory = L2A::UTIL::ClearTemporaryDirectory();

    // Test that we can create a Latex document with a unicode path
    TestLatexBase(ut, temp_directory);

    L2A::UTIL::SetWorkingDirectory(L2A::UTIL::FilePathStdToAi(old_cwd));

    // Test that header inclusions work.
    TestHeader(ut, temp_directory);

    // Test the strip comments functionality.
    TestStripComments(ut);
}
