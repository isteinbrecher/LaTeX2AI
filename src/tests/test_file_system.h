// -----------------------------------------------------------------------------
// MIT License
//
// Copyright (c) 2020-2025 Ivo Steinbrecher
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


#ifndef TEST_FILE_H_
#define TEST_FILE_H_


// Forward declarations.
namespace L2A
{
    namespace TEST
    {
        namespace UTIL
        {
            class UnitTest;
        }
    }  // namespace TEST
}  // namespace L2A


namespace L2A
{
    namespace TEST
    {
        /**
         * \brief Test the functionality of the file system functions.
         */
        void TestFileSystem(L2A::TEST::UTIL::UnitTest& ut);
    }  // namespace TEST
}  // namespace L2A

#endif
